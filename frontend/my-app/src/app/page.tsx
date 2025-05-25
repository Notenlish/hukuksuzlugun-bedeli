"use client";
import { TypographyP, TypographyH1 } from "@/components/ui/typography";
import Link from "next/link";
import AllChanges from "@/components/changes/AllChanges";

import { differenceItem } from "@/types";
import { useEffect, useState } from "react";

export default function Home() {
  const [differences, setDifferences] = useState<differenceItem[]>([
    {
      type: "DAILY_USD_TRY",
      format_template:
        "Dolar <span class='text-green-700 font-bold'>{changePercentage}%</span> arttı, {startValue}{den} <b>{endValue}{e}</b> vardı.",
      changePercentage: 6.02,
      startValue: 36.61,
      endValue: 38.75,
    },
    {
      type: "DAILY_EUR_TRY",
      format_template:
        "Euro <span class='text-sky-600 font-bold'>{changePercentage}%</span> arttı, {startValue}{den} <b>{endValue}{e}</b> vardı.",
      changePercentage: 9.63,
      startValue: 40.09,
      endValue: 43.82,
    },
    {
      type: "MONTHLY_CPI",
      format_template:
        "TÜFE <span class='text-red-700 font-bold'>{changePercentage}%</span> arttı, {startValue}{den} <b>{endValue}{e}</b> vardı.",
      changePercentage: 0,
      startValue: 0,
      endValue: 0,
    },
    {
      type: "INTEREST(WEEKLY)",
      format_template:
        "Faiz <span class='text-orange-700 font-bold'>{changePercentage}%</span> arttı, {startValue}{den} <b>{endValue}{e}</b> vardı.",
      changePercentage: 0,
      startValue: 0,
      endValue: 0,
    },
  ]);

  useEffect(() => {
    console.log(differences);
    const _ = async () => {
      const res = await fetch("/api/get-data");
      if (res.ok) {
        const data = await res.json();

        const updatedDifferences = differences.map((e) => {
          if (data[e.type]) {
            const o = data[e.type];
            for (const [key, value] of Object.entries(o)) {
              // @ts-expect-error 7053
              e[key] = value;
            }
          }
          return e;
        });

        setDifferences(updatedDifferences);
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
        <div className="w-full text-center"><TypographyP>
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
        </TypographyP></div>
      </main>
      <footer className="row-start-3 flex gap-[24px] flex-wrap items-center justify-center"></footer>
    </div>
  );
}
