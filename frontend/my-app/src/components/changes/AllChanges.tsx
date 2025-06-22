// import { TypographyP } from "../ui/typography";
import parse from "html-react-parser";

import { differenceItem } from "@/types";
import { den_dan_eki, e_a_eki } from "@/lib/utils";
import { Skeleton } from "@/components/ui/skeleton";
import { roundToNthDecimal } from "@/lib/utils";


function evaluateTemplateExpressions(
  template: string,
  context: Record<string, number>,
): string {
  const functionRegex = /(round|neg|dotted_num|no_trailing_zeroes)\(([^\(\)]+?)\)/;

  while (functionRegex.test(template)) {
    template = template.replace(functionRegex, (_, funcName, inner) => {
      let result: number | string;

      // Recursively resolve inner expressions
      const resolvedInner = evaluateTemplateExpressions(inner, context);

      if (funcName === "neg") {
        const val = getValue(resolvedInner, context);
        result = -val;
      } else if (funcName === "round") {
        const [valueExpr, decimalExpr] = resolvedInner
          .split(",")
          .map((s) => s.trim());
        const val = getValue(valueExpr, context);
        const decimals = parseInt(decimalExpr, 10);
        result = roundToNthDecimal(val, decimals);
      } else if (funcName === "dotted_num") {
        // This DOES NOT handle for dots(float values)
        // you must round it beforehand
        const [valueExpr] = resolvedInner.split(",").map((s) => s.trim());
        const val = getValue(valueExpr, context);

        // instead of starting at the start, start from the end
        const charArr = val.toString().split("").reverse();
        const newArr = [];
        let part = [];
        for (let i = 0; i < charArr.length; i++) {
          const curChar = charArr[i];
          part.push(curChar);
          if (part.length == 3) {
            newArr.push(part.reverse().join(""));
            part = [];
          } else {
            if (i === charArr.length-1){
              newArr.push(part.reverse().join(""));
              part = [];
            }
          }
        }
        result = newArr.reverse().join(".");
      } else if (funcName == "no_trailing_zeroes") {
        const val = getValue(resolvedInner, context);
        result = parseFloat(val.toString());
      } else {
        throw new Error(`Unknown function: ${funcName}`);
      }
      if (typeof result == "string") {
        return result;
      } else {
        return result.toString();
      }
    });
  }

  return template;
}

function getValue(expr: string, context: Record<string, number>): number {
  if (/^-?\d+(\.\d+)?$/.test(expr)) return parseFloat(expr);
  if (expr in context) return context[expr];
  throw new Error(`Unknown variable or expression: "${expr}"`);
}


export default function AllChanges({
  differences,
  loaded,
}: {
  differences: differenceItem[];
  loaded: boolean;
}) {
  return (
    <div className="block text-center w-full">
      {loaded ? (
        differences.map((d, i) => {
          const copyOfD = JSON.parse(JSON.stringify(d));

          let text = d.formatTemplate;

          // check for negative multipliers in templating
          const negFormattables = [
            { format: "{-changeValue}", key: "changeValue" },
            { format: "{-changePercentage}", key: "changePercentage" },
            { format: "{-startValue}", key: "startValue" },
            { format: "{-endValue}", key: "endValue" },
          ];
          for (const f of negFormattables) {
            if (text.includes(f.format)) {
              text = text.replace(f.format, f.format.replace("-", ""));

              // @ts-expect-error 7053
              const negative_val = d[f.key] * -1;
              copyOfD[f.key] = negative_val;
            }
          }

          text = evaluateTemplateExpressions(text, {
            changeValue: d.changeValue || 0,
            changePercentage: d.changePercentage || 0,
            startValue: d.startValue || 0,
            endValue: d.endValue || 0,
          });

          text = text
            .replaceAll("{dan}", "{den}")
            .replaceAll("{a}", "{e}")
            .replace(
              "{changeValue}",
              roundToNthDecimal(copyOfD.changeValue as number, 2).toString(),
            )
            .replace(
              "{changePercentage}",
              roundToNthDecimal(
                copyOfD.changePercentage as number,
                2,
              ).toString(),
            )
            .replace(
              "{startValue}",
              roundToNthDecimal(copyOfD.startValue as number, 2).toString(),
            )
            .replace(
              "{endValue}",
              roundToNthDecimal(copyOfD.endValue as number, 2).toString(),
            );

          while (text.includes("{den}")) {
            const last = text.slice(
              text.indexOf("{den}") - 1,
              text.indexOf("{den}"),
            );
            text = text.replace("{den}", den_dan_eki(last));
          }
          while (text.includes("{e}")) {
            const last = text.slice(
              text.indexOf("{e}") - 1,
              text.indexOf("{e}"),
            );
            text = text.replace("{e}", e_a_eki(last));
          }

          return (
            <p className="leading-8 text-xl" key={i}>
              {parse(text)} <br />
            </p>
          );
        })
      ) : (
        <Skeleton className="w-full h-64"></Skeleton>
      )}
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
