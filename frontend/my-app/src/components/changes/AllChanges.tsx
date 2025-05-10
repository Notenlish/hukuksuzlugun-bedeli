import { TypographyP } from "../ui/typography";

interface differenceItem {
  format_template: string;
  changeValue?: number;
  changePerc?: number;
  startValue?: number;
  endValue?: number;
}

export default function AllChanges({
  differences,
}: {
  differences: differenceItem[];
}) {
  return <>
    {differences.map((d) => {
      const text = d.format_template.repl
    })}
  </>;
}
