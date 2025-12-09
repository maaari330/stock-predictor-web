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
        <div className="w-md px-4 ml-2 mr-10 border-double border-sky-200">
          {PredictionLabel=="UP"?(
            <p className={"font-semibold text-green-300"}>明日の株価予測：{PredictionLabel}<BsGraphUpArrow/></p>
          ):(
            <p className={"font-semibold text-red-300"}>明日の株価予測：{PredictionLabel}<BsGraphDownArrow/></p>
          )}
          <p>予測精度：{Confidence*100}%</p>
          <progress value={Confidence*100} max={100} />
        </div>
      }
    </>
  );
}
