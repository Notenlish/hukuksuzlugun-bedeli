"use client";

import { useState, useEffect } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { TypographyH3 } from "../ui/typography";

interface TimeUnit {
  value: number;
  label: string;
}

interface AnimatedNumberProps {
  value: number;
  digits: number;
}

function AnimatedNumber({ value, digits }: AnimatedNumberProps) {
  const [displayValue, setDisplayValue] = useState(value);
  const [isAnimating, setIsAnimating] = useState(false);

  useEffect(() => {
    if (value !== displayValue) {
      setIsAnimating(true);
      const timer = setTimeout(() => {
        setDisplayValue(value);
        setIsAnimating(false);
      }, 150);
      return () => clearTimeout(timer);
    }
  }, [value, displayValue]);

  const formattedValue = value.toString().padStart(digits, "0");
  const formattedDisplayValue = displayValue.toString().padStart(digits, "0");

  return (
    <div className="relative overflow-hidden">
      <div
        className={`transition-transform duration-300 ease-in-out ${
          isAnimating
            ? "transform translate-y-full opacity-0"
            : "transform translate-y-0 opacity-100"
        }`}
      >
        <span className="font-mono text-4xl md:text-6xl font-bold tabular-nums">
          {formattedDisplayValue}
        </span>
      </div>
      {isAnimating && (
        <div className="absolute inset-0 transform -translate-y-full animate-slide-down">
          <span className="font-mono text-4xl md:text-6xl font-bold tabular-nums">
            {formattedValue}
          </span>
        </div>
      )}
    </div>
  );
}

export default function CounterTimer({
  title,
  description,
  startDate,
}: {
  title: string;
  description: string;
  startDate: Date;
}) {
  const [timeUnits, setTimeUnits] = useState<TimeUnit[]>([
    { value: 0, label: "Months" },
    { value: 0, label: "Days" },
    { value: 0, label: "Hours" },
    { value: 0, label: "Minutes" },
    { value: 0, label: "Seconds" },
  ]);

  useEffect(() => {
    const calculateTimeElapsed = () => {
      const now = new Date().getTime();
      const start = startDate.getTime();
      const difference = now - start; // Calculate elapsed time

      if (difference >= 0) {
        // Ensure difference is non-negative
        const months = Math.floor(difference / (1000 * 60 * 60 * 24 * 30.44));
        const days = Math.floor(
          (difference % (1000 * 60 * 60 * 24 * 30.44)) / (1000 * 60 * 60 * 24),
        );
        const hours = Math.floor(
          (difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60),
        );
        const minutes = Math.floor(
          (difference % (1000 * 60 * 60)) / (1000 * 60),
        );
        const seconds = Math.floor((difference % (1000 * 60)) / 1000);

        setTimeUnits([
          { value: months, label: "Ay" },
          { value: days, label: "Gün" },
          { value: hours, label: "Saat" },
          { value: minutes, label: "Dakika" },
          { value: seconds, label: "Saniye" },
        ]);
      }
    };

    calculateTimeElapsed();
    const interval = setInterval(calculateTimeElapsed, 1000);

    return () => clearInterval(interval);
  }, [startDate]);

  return (
    <div className="w-full max-w-6xl mx-auto p-4">
      <Card className="bg-gradient-to-br from-red-700 to-red-900">
        <CardContent className="p-8">
          <div className="text-center mb-0">
            <p className="text-slate-100">
              {description} {startDate.toLocaleDateString()}
            </p>
            <h1 className="text-3xl md:text-4xl font-extrabold text-white mt-3 mb-2">
              {title}
            </h1>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 md:gap-6">
            {timeUnits.map((unit, index) => (
              <div key={unit.label} className="text-center">
                {/* bg-slate-800/50 border-slate-600 */}
                <Card className="bg-transparent shadow-none border-none backdrop-blur-sm">
                  <CardContent className="p-4 md:p-2">
                    <div className="mb-2 min-h-[4rem] md:min-h-[6rem] flex items-center justify-center">
                      <AnimatedNumber
                        value={unit.value}
                        digits={index === 0 ? 2 : 2}
                      />
                    </div>
                    <div className="text-red-100 text-lg md:text-base font-medium uppercase tracking-wider">
                      {unit.label}
                    </div>
                  </CardContent>
                </Card>
              </div>
            ))}
          </div>
          <div className="w-full text-center text-white">
            <TypographyH3>Geçti.</TypographyH3>
          </div>

          <div className="mt-8 text-center">
            <div className="inline-flex items-center space-x-2 text-base text-gray-100">
              <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
              <span>Canlı Sayaç</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
