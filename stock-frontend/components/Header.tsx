'use client'

import { usePathname } from "next/navigation"

export default function Header() {
    const pathname = usePathname();

    const isAdmin = pathname === "/admin" || pathname.startsWith("/admin/")
    const headerText = isAdmin ? "あしたの株ラボ" : "あしたの株ラボ"

    return <header className="site-header">{headerText}</header>
}