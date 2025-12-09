'use client'
import { useState } from "react";
import { BsGraphUpArrow } from "react-icons/bs";
import { BsGraphDownArrow } from "react-icons/bs";

export default function Home() {
  const [Ticker,setTicker]=useState("")
  const [PredictionLabel,setPredictionLabel]=useState("")
  const [Confidence,setConfidence]=useState(0)


  async function handleSubmit(e: React.FormEvent<HTMLFormElement>){
    e.preventDefault();
    const res=await fetch('http://localhost:8000/predict',{method:'POST',headers: {'Content-Type': 'application/json'},body:JSON.stringify({Ticker:Ticker})})
    const resBody= await res.json()
    setPredictionLabel(resBody.PredictionLabel)
    setConfidence(resBody.Confidence)
  }

  return (
    <>
      <div>
        株価予測アプリ
      </div>
      <form method="post" onSubmit={handleSubmit}>
        <label>
          銘柄コード/Ticker:
          <input type="text" name="ticker" value={Ticker} onChange={e => setTicker(e.target.value)}/>
        </label>
        <button type="submit">株価予測</button>
      </form>
      {PredictionLabel && 
        <div style={{border:"solid",padding:"1rem 2rem", width:"fit-content",margin:"2rem auto"}}>
          <p style={{color: PredictionLabel=="UP"?"green":"red",fontWeight:"bold"}}>明日の株価予測：{PredictionLabel}{PredictionLabel=="UP"?<BsGraphUpArrow/>:<BsGraphDownArrow/>}</p>
          <p>予測精度：{Confidence*100}%</p>
          <progress value={Confidence*100} max={100} />
        </div>
      }
    </>
  );
}
