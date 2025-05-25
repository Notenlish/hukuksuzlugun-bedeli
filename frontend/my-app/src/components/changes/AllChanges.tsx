// import { TypographyP } from "../ui/typography";
import parse from "html-react-parser";

import { differenceItem } from "@/types";
import { den_dan_eki, e_a_eki } from "@/lib/utils";

export default function AllChanges({
  differences,
}: {
  differences: differenceItem[];
}) {
  const roundToNthDecimal = (num: number, n: number) => {
    const factor = Math.pow(10, n);
    return Math.round((num + Number.EPSILON) * factor) / factor;
  };
  return (
    <div className="block text-center w-full">
      {differences.map((d, i) => {
        let text = d.format_template
          .replaceAll("{dan}", "{den}")
          .replaceAll("{a}", "{e}")
          .replace("{changeValue}", roundToNthDecimal(d.changeValue as number, 2).toString())
          .replace(
            "{changePercentage}",
            roundToNthDecimal(d.changePercentage as number, 2).toString(),
          )
          .replace("{startValue}", roundToNthDecimal(d.startValue as number, 2).toString())
          .replace("{endValue}", roundToNthDecimal(d.endValue as number, 2).toString());

        while (text.includes("{den}")) {
          const last = text.slice(
            text.indexOf("{den}") - 1,
            text.indexOf("{den}"),
          );
          text = text.replace("{den}", den_dan_eki(last));
        }
        while (text.includes("{e}")) {
          const last = text.slice(text.indexOf("{e}") - 1, text.indexOf("{e}"));
          text = text.replace("{e}", e_a_eki(last));
        }

        return (
          <p className="leading-8 text-xl" key={i}>
            {parse(text)} <br />
          </p>
        );
      })}
      {/*
        dolar %10 arttı, 36'dan 38'e vardı
        Faiz %42.5'den %46'ya çıktı
        Dış borç 500 milyar tl oldu
        100 milyar dolar ülkeden çıkış yaptı
        57 Milyar Dolar döviz rezervi sattık
      */}
    </div>
  );
}
