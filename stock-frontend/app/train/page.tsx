'use client'
import { useState } from "react";

export default function Management() {
    type ModelInfo = { id: number, ticker: string, fx: string, trained_at: string, threshold: number }
    const [Ticker, setTicker] = useState("")
    const [TickerSymbol, setTickerSymbol] = useState("")
    const [Models, setModels] = useState<ModelInfo[]>([])

    async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault();
        const api_train_url = `${process.env.NEXT_PUBLIC_HOST}/api/train/`
        await fetch(api_train_url, {
            method: 'POST',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ticker: Ticker, fx: TickerSymbol })
        })
    }

    async function getModelsList() {
        const response = await fetch(`${process.env.NEXT_PUBLIC_HOST}/api/train/show/`, {
            method: "GET",
            credentials: "include",
        });
        const models_list = await response.json();
        setModels(models_list);
    }

    const formatJST = (iso: string) =>
        new Date(iso).toLocaleString("ja-JP", { timeZone: "Asia/Tokyo" });

    return (
        <main className="page">
            <h2 className="pageHeader">
                株価予測モデル作成
            </h2>
            <form method="post" onSubmit={handleSubmit} className="forms">
                <label>
                    銘柄コード/Ticker:
                    <input type="text" required value={Ticker} onChange={e => setTicker(e.target.value)} />
                </label>
                <label>
                    ティッカーシンボル/Ticker Symbol:
                    <input type="text" required value={TickerSymbol} onChange={e => setTickerSymbol(e.target.value)} />
                </label>
                <button type="submit" className="btn">モデル作成</button>
            </form>
            <h2 className="pageHeader">保存済みモデル一覧</h2>
            <button type="button" className="btn" onClick={getModelsList}>
                一覧更新
            </button>
            <table className="tbl">
                <thead>
                    <tr>
                        <th>id</th>
                        <th>銘柄コード</th>
                        <th>為替</th>
                        <th>モデル作成日時</th>
                        <th>しきい値</th>
                    </tr>
                </thead>
                <tbody>
                    {Models.map(m => (
                        <tr key={m.id}>
                            <td>{m.id}</td>
                            <td>{m.ticker} </td>
                            <td>{m.fx}</td>
                            <td>{formatJST(m.trained_at)}</td>
                            <td>{m.threshold}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </main>
    );
}