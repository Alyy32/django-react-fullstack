import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Wisecool Parent App',
  description: 'Django + Next.js Full-Stack Application',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
