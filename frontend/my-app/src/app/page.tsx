"use client";
import {
  TypographyP,
  TypographyH3,
  TypographyH2,
} from "@/components/ui/typography";
import Link from "next/link";
// import AllChanges from "@/components/changes/AllChanges";
import AllChanges2 from "@/components/changes/AllChanges2";

// import { differenceItem } from "@/types";
import { useEffect, useState } from "react";
import CounterTimer from "@/components/counter/counter-timer";
import Quotes from "@/components/quotes/quotes";
import { Change } from "@/types";

export default function Home() {
  const [loaded, setLoaded] = useState(false);
  /*
  chart-1 = red
  chart-2 = emerald
  chart-3 = darkgreen
  chart-4 = blue
  chart-5 = orange
  */
  const [changes, setChanges] = useState<Change[]>([
    {
      graph: [],
      color:"chart-2",
      textColor:"text-emerald-700",
      title: "Dolar",
      type: "DAILY_USD_TRY",
      formatTemplate:
        "Dolar <span class='text-green-700 font-bold'>%{changePercentage}</span> arttı, {startValue}{den} <b>{endValue}{e}</b> vardı.",
      changePercentage: 6.02,
      startValue: 36.61,
      endValue: 38.75,
    },
    {
      graph: [],
      color:"chart-4",
      textColor:"text-blue-500",
      title: "Avro",
      type: "DAILY_EUR_TRY",
      formatTemplate:
        "Euro <span class='text-sky-600 font-bold'>%{changePercentage}</span> arttı, {startValue}{den} <b>{endValue}{e}</b> vardı.",
      changePercentage: 9.63,
      startValue: 40.09,
      endValue: 43.82,
    },
    {
      graph: [],
      color: "chart-1",
      textColor:"text-red-500",
      title: "TÜFE",
      type: "MONTHLY_CPI",
      formatTemplate:
        "TÜFE <span class='text-red-700 font-bold'>%{changePercentage}</span> arttı, {startValue}{den} <b>{endValue}{e}</b> vardı.",
      changePercentage: 0,
      startValue: 0,
      endValue: 0,
    },
    {
      graph: [],
      title: "Faiz",
      color:"chart-1",
      textColor:"text-red-500",
      type: "INTEREST(WEEKLY)",
      formatTemplate:
        "Tüketici Kredisi Faiz Oranları <span class='text-orange-700 font-bold'>%{changePercentage}</span> arttı, %{startValue}{den} <b>%{endValue}{e}</b> vardı.",
      changePercentage: 0,
      startValue: 0,
      endValue: 0,
    },
    {
      graph: [],
      title: "Brüt Rezervler",
      color:"chart-1",
      textColor:"text-red-500",
      type: "GROSS RESERVES(USD)",
      formatTemplate:
        "Brüt Rezervler <span class='text-red-500 font-bold'>% round(neg(changePercentage),2)</span> azaldı, no_trailing_zeroes(dotted_num(round(startValue,-2))) Milyar Dolar{dan} <b>no_trailing_zeroes(dotted_num(round(endValue,-2))) Milyar Dolar{a}</b> vardı.",
      changePercentage: 0,
      startValue: 0,
      endValue: 0,
    },
  ]);

  useEffect(() => {
    const _ = async () => {
      const res = await fetch("/api/get-data");
      if (res.ok) {
        let data;
        try {
          data = await res.json();
          // console.log("DATA GOT:", data);
        } catch (err) {
          console.error("AAA", err);
        }
        const updatedChanges = changes.map((e) => {
          if (data[e.type]) {
            const o = data[e.type];
            for (const [key, value] of Object.entries(o)) {
              e[key] = value;
            }
          }
          return e;
        });

        setChanges(updatedChanges);
        setLoaded(true);
      }
    };
    _();
  }, []);

  // Date İmamoğlu Arrested as unix timestamp
  const unixEpochTimeMS = 1742357575 * 1000;
  const startDate = new Date(unixEpochTimeMS);

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
        {/* UNIX Epoch Time of 19th of March, 07:12, 2025, Turkey Timezone(UTC+03) */}
        <CounterTimer
          title="İmamoğlu'nun Haksızca Tutuklanmasından Beri:"
          description="İmamoğlu'nun tutuklandığı Tarih"
          startDate={startDate}
        />
        <div className="text-center w-full">
          <TypographyH3>
            İmamoğlu&apos;nun Haksızca Tutuklanmasının Türkiye&apos;e Maliyeti:
          </TypographyH3>
        </div>
        {/* <AllChanges loaded={loaded} differences={changes} /> */}
        <AllChanges2 loaded={loaded} changes={changes}></AllChanges2>
        <div className="w-full text-lg text-center">
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
        </div>
        <br></br>
        <TypographyH2>Önemli Haberler</TypographyH2>
        <Quotes></Quotes>
      </main>
      <footer className="row-start-3 flex gap-[24px] flex-wrap items-center justify-center"></footer>
    </div>
  );
}
