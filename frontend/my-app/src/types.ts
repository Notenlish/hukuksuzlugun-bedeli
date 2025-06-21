export interface differenceItem {
  type: string;
  format_template: string;
  changeValue?: number;
  changePercentage?: number;
  startValue?: number;
  endValue?: number;
}

export interface QuoteData {
  author: string;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  image: any;
  text: string;
  source: string;
  date: Date;
}
