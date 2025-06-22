"use client";

import {
  // ResponsiveContainer,
  CartesianGrid,
  // Line,
  // LineChart,
  XAxis,
  YAxis,
  Area, // Import Area for the gradient fill
  AreaChart, // Important: Use AreaChart if you're primarily showing an area
} from "recharts";

import {
  //Card,
  CardContent,
  //CardDescription,
  //CardFooter,
  //CardHeader,
  //CardTitle,
} from "@/components/ui/card";

import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "../ui/chart";
import { Change } from "@/types";

export const description = "A linear area chart with gradient fill";

export function ChangeChart({ change, id }: { change: Change; id: number }) {
  const areaGradientId = `areaGradient-${id}`;

  const chartData = change.graph.map((e) => {
    return { date: e.date, value: e.value };
  });

  const chartConfig = {
    value: {
      label: `${change.title}`,
      color: `var(--${change.color})`,
    },
  } satisfies ChartConfig;

  return (
    <div className="mt-8">
      <CardContent className="">
        <ChartContainer className="h-64 w-full" config={chartConfig}>
          <AreaChart // Switched to AreaChart to better support the area fill
            height={64}
            accessibilityLayer
            data={chartData}
            margin={{
              left: 12,
              right: 12,
            }}
          >
            <CartesianGrid vertical={false} />
            <YAxis
              domain={[change.startValue ?? 0, change.endValue ?? 100].sort(
                (a, b) => a - b,
              )}
            />
            <XAxis
              dataKey="date"
              tickLine={false}
              axisLine={false}
              tickMargin={8}
              tickFormatter={(value) => {
                const d = new Date(value);
                return d.toLocaleDateString(navigator.language, {
                  month: "short",
                  day: "numeric",
                });
              }}
            />
            <ChartTooltip
              cursor={false}
              content={<ChartTooltipContent hideLabel />}
            />
            <defs>
              {/* Define the linear gradient for the fill */}
              <linearGradient id={areaGradientId} x1="0" y1="0" x2="0" y2="1">
                <stop
                  offset="5%"
                  stopColor={`var(--color-${change.color})`} // Top of the gradient
                  stopOpacity={0.7}
                />
                <stop
                  offset="95%"
                  stopColor={`var(--color-${change.color})`} // Bottom of the gradient
                  stopOpacity={0.1}
                />
              </linearGradient>
            </defs>
            <Area
              dataKey="value"
              type="linear"
              fill={`url(#${areaGradientId})`} // Apply the gradient to the fill property
              fillOpacity={1} // Ensure fill is visible
              stroke={`var(--color-${change.color})`} // Keep the line stroke visible with the primary color
              strokeWidth={2}
              dot={false}
            />
          </AreaChart>
        </ChartContainer>
      </CardContent>
    </div>
  );
}
