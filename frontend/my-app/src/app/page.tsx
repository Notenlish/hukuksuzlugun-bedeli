import {
  TypographyP,
  TypographyH1,
  TypographyH2,
} from "@/components/ui/typography";
import AllChanges from "@/components/changes/AllChanges";

import { differenceItem } from "@/types";
import { den_dan } from "@/lib/utils";

export default function Home() {
  const differences: differenceItem[] = [
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
  ];
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
        <TypographyH2>İmamoğlu Haksızca Tutuklandıktan Beri:</TypographyH2>
        <AllChanges differences={differences} />
      </main>
      <footer className="row-start-3 flex gap-[24px] flex-wrap items-center justify-center"></footer>
    </div>
  );
}
