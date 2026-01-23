
type Props = {
    title: string;
    children: React.ReactNode;
}

export default function PageLayout({ title, children }: Props) {
    return (
        <main>
            <h1>{title}</h1>
            {children}
        </main>
    )
}