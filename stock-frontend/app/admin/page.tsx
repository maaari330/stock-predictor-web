'use client'
import { useState } from "react";

export default function Management() {
    const [Ticker, setTicker] = useState("")
    const [TickerSymbol, setTickerSymbol] = useState("")

    async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault();
        const admin_api_url = `${process.env.NEXT_PUBLIC_HOST} /admin/`
        await fetch(admin_api_url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ticker: Ticker, fx: TickerSymbol })
        })
    }
    return (
        <main>
            <div>
                株価予測アプリ 管理画面
            </div>
            <form method="post" onSubmit={handleSubmit} className="forms">
                <label>
                    銘柄コード/Ticker:
                    <input type="text" required value={Ticker} onChange={e => setTicker(e.target.value)} />
                </label>
                <label>
                    ティッカーシンボル/Ticker Symbol:
                    <input type="text" required value={TickerSymbol} onChange={e => setTickerSymbol(e.target.value)} />
                </label>
                <button type="submit">株価予測モデル作成</button>
            </form>
        </main>
    );
}