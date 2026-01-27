import type { Metadata } from "next";
import Header from "../components/Header"
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "あしたの株価ラボ",
  description: "株価予測のモデル作成、作成したモデルを使用した翌営業日の株価上昇・下落確率を予測できるサイト",
};

export default function RootLayout({ children, }: Readonly<{ children: React.ReactNode; }>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <Header />
        <div className="container">
          {children}
        </div>
      </body>
    </html>
  );
}
