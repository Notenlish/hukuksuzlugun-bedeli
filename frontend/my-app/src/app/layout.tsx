import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { TypographyH1 } from "@/components/ui/typography";
import Link from "next/link";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Hukuksuzluğun Bedeli - İmamoğlu'nun Tutuklanmasının Maliyeti",
  description: "İmamoğlu'nun Tutuklanmasının Maliyetini günlük ölçen bir site",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <header className="flex items-center justify-center py-4">
          <Link className="hover:underline" href="/">
            <TypographyH1>Hukuksuzluğun Maliyeti</TypographyH1>
          </Link>
        </header>
        {children}
        <footer className="flex items-center justify-center justify-center py-4">
          <Link className="hover:underline" href="/contact">İletişim</Link>
        </footer>
      </body>
    </html>
  );
}
