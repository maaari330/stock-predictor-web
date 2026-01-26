'use client'
import Plot from "react-plotly.js"
import { useState } from "react";

export default function StockChart({ ticker }: { ticker: string }) {
    type Metric = "Close" | "Volatility" | "MA_Ratio"
    const [Metrics, setMetrics] = useState<Metric>("Close")
    const [Start, setStart] = useState("")
    const [End, setEnd] = useState("")
    const [MetricDates, setMetricDates] = useState([])
    const [MetricValues, setMetricValues] = useState([])

    async function handleMetricsGet(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault();
        const metrics_api_url = `${process.env.NEXT_PUBLIC_HOST}/api/stock_series/?ticker=${ticker}&metric=${Metrics}&start=${Start}&end=${End}`
        const response = await fetch(metrics_api_url, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
        })
        const response_body = await response.json()
        setMetricDates(response_body.dates)
        setMetricValues(response_body.values)
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
                    開始期間～終了期間
                    <div className="dateRow">
                        <input type="date" value={Start} required onChange={e => setStart(e.target.value)}></input>
                        <span>~</span>
                        <input type="date" value={End} required onChange={e => setEnd(e.target.value)}></input>
                    </div>
                </label>
                <button type="submit" className="btn">株価情報取得</button>
            </form>
            <Plot
                data={[
                    {
                        x: MetricDates,
                        y: MetricValues,
                        type: 'scatter',
                        mode: 'lines+markers',
                        marker: { color: 'red' },

                    },
                ]}
                layout={{ title: { text: ticker + "-" + Metrics }, xaxis: { tickangle: 90 }, }}
                style={{ width: "100%", height: "400px" }}
                useResizeHandler={true}
            />
        </div>
    );
}