"use client";
import { TypographyP, TypographyH1 } from "@/components/ui/typography";
import Link from "next/link";
import AllChanges from "@/components/changes/AllChanges";

import { differenceItem } from "@/types";
import { useEffect, useState } from "react";

export default function Home() {
  // differenceItem[]
  const [differences, setDifferences] = useState([
    {
      format_template:
        "Dolar {changePerc} arttı, {startValue}{den} {endValue}{e} vardı.",
      changePerc: "% 10",
      startValue: 36,
      endValue: 38.75,
    },
    {
      format_template:
        "Dolar {changePerc} arttı, {startValue}{den} {endValue}{e} vardı.",
      changePerc: "% 10",
      startValue: 36,
      endValue: 38.75,
    },
  ]);

  useEffect(() => {
    console.log(differences)
    const _ = async () => {
      const res = await fetch("/api/get-data");
      if (res.ok) {
        const data = await res.json();
        differences[0].startValue = data["dollarChange"]["old"];
        differences[0].endValue = data["dollarChange"]["new"];
      }
    };
    _();
  }, []);

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
        <TypographyH1>İmamoğlu Haksızca Tutuklandıktan Beri:</TypographyH1>
        {/*
          */}
         <AllChanges differences={differences} />
        <TypographyP>
          İmamoğlu&apos;na özgürlük için imza verebilirsiniz:{" "}
          <Link
            className="text-red-600 font-bold hover:underline"
            href="https://imza.chp.org.tr/"
          >
            İmza Kampanyası
          </Link>
          <br />
          Poster ve Afişler:{" "}
          <Link
            className="text-red-600 font-bold hover:underline"
            href="https://drive.google.com/drive/u/0/folders/1PGxXcipSYx7LxTgUUiJ_hmd0HLT7girr"
          >
            İmamoğlu Poster ve Afiş Tasarımları
          </Link>
        </TypographyP>
      </main>
      <footer className="row-start-3 flex gap-[24px] flex-wrap items-center justify-center"></footer>
    </div>
  );
}
