import { Change } from "@/types";
import { TypographyH3 } from "../ui/typography";
import { ArrowUp } from "lucide-react";
import { roundToNthDecimal } from "@/lib/utils";
import { ChangeChart } from "./ChangeChart";

export default function ChangeComponent({ change,id }: { change: Change,id:number }) {
  console.log("change bu",change, "amın evladı")
  return (
    <div className="w-full">
      {/* Needed to get tailwind to actually include the color variables */}
      <div className="none skibidiIncludeColorCharts">
      </div>
      <div className="flex justify-between w-full">
        <TypographyH3>{change.title}</TypographyH3>
        <div className={`flex ${change.textColor}`}>
          <ArrowUp size={32} />
          <div>%{roundToNthDecimal(change.changePercentage as number, 2)}</div>
        </div>
      </div>
      <ChangeChart id={id} change={change}></ChangeChart>
    </div>
  );
}
