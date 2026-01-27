'use client'

import { usePathname } from "next/navigation"

export default function Header() {
    const pathname = usePathname();

    const isAdmin = pathname === "/admin" || pathname.startsWith("/admin/")
    const headerText = isAdmin ? "トヨタ株予測サイト 管理者用" : "トヨタ株予測サイト"

    return <header className="site-header">{headerText}</header>
}