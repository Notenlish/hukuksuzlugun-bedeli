import { BRAND } from "zod";
import { TypographyP } from "../ui/typography";

import { differenceItem } from "@/types";
import { den_dan_eki, e_a_eki } from "@/lib/utils";

export default function AllChanges({
  differences,
}: {
  differences: differenceItem[];
}) {
  return (
    <div className="block text-center w-full">
      {differences.map((d, i) => {
        let text = d.format_template
          .replaceAll("{dan}", "{den}")
          .replaceAll("{a}", "{e}")
          //@ts-expect-error ...
          .replace("{changeValue}", d.changeValue)
          //@ts-expect-error ...
          .replace("{changePerc}", d.changePerc)
          //@ts-expect-error ...
          .replace("{startValue}", d.startValue)
          //@ts-expect-error ...
          .replace("{endValue}", d.endValue);

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
          <div key={i}>
            {text} <br />
          </div>
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
