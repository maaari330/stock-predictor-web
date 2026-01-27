'use client'
import Plot from "react-plotly.js"
import { useState } from "react";

export default function StockChart() {
    type Metric = "Close" | "Volatility" | "MA_Ratio"
    const [Metrics, setMetrics] = useState<Metric>("Close")
    const [ChartTicker, setChartTicker] = useState("")
    const [Start, setStart] = useState("")
    const [End, setEnd] = useState("")
    const [Competitor, setCompetitor] = useState("7267.T")
    const [MainDates, setMainDates] = useState([])
    const [MainValues, setMainValues] = useState([])
    const [CompetitorDates, setCompetitorDates] = useState([])
    const [CompetitorValues, setCompetitorValues] = useState([])

    async function handleMetricsGet(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault();
        const metrics_api_url = `${process.env.NEXT_PUBLIC_HOST}/api/stock_series/?ticker=${ChartTicker}&metric=${Metrics}&start=${Start}&end=${End}&competitor=${Competitor}`
        const response = await fetch(metrics_api_url, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
        })
        const response_body = await response.json()
        const response_competitor = response_body["competitor"]
        setMainDates(response_body["main"].dates)
        setMainValues(response_body["main"].values)
        if (response_competitor) {
            setCompetitorDates(response_competitor.dates)
            setCompetitorValues(response_competitor.values)
        }
        else {
            setCompetitorDates([])
            setCompetitorValues([])
        }
    }

    const traces: any[] = [{
        x: MainDates, y: MainValues, type: 'scatter', mode: 'lines+markers', name: ChartTicker, marker: { color: 'red' },
    }]

    if (CompetitorDates.length > 0) {
        traces.push({
            x: CompetitorDates, y: CompetitorValues, type: 'scatter', mode: 'lines+markers', name: Competitor, marker: { color: 'green' },
        })
    }

    return (
        <div>
            <form onSubmit={handleMetricsGet} className="forms">
                <select value={Metrics} onChange={e => setMetrics(e.target.value as Metric)}>
                    <option value="Close">Close</option>
                    <option value="Volatility">Volatility</option>
                    <option value="MA_Ratio">MA_Ratio</option>
                </select>
                <label>
                    銘柄コード/Ticker:
                    <input type="text" required value={ChartTicker} onChange={e => setChartTicker(e.target.value)} />
                </label>
                <label>
                    開始期間～終了期間
                    <div className="dateRow">
                        <input type="date" value={Start} required onChange={e => setStart(e.target.value)}></input>
                        <span>~</span>
                        <input type="date" value={End} required onChange={e => setEnd(e.target.value)}></input>
                    </div>
                </label>
                <label>
                    他社比較:
                    <input type="text" value={Competitor} onChange={e => setCompetitor(e.target.value)} />
                </label>
                <button type="submit" className="btn">株価情報取得</button>
            </form>
            <Plot
                data={traces}
                layout={{ title: { text: ChartTicker + "-" + Metrics }, xaxis: { tickangle: 90 }, }}
                style={{ width: "100%", height: "400px" }}
                useResizeHandler={true}
            />
        </div>
    );
}