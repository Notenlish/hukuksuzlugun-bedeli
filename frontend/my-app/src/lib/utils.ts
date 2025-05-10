import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function den_dan_eki(text: string) {
  const e_suffix_letters = ["1", "2", "3", "4", "5", "7", "8"];
  if (e_suffix_letters.includes(text.slice(text.length - 1))) {
    return "'den";
  }
  return "'dan";
}

export function e_a_eki(text: string) {
  const e_suffix_letters = ["1", "2", "3", "4", "5", "7", "8"];
  if (e_suffix_letters.includes(text.slice(text.length - 1))) {
    return "'e";
  }
  return "'a";
}
