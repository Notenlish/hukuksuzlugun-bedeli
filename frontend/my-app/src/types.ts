export interface differenceItem {
  type: string;
  formatTemplate: string;
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

export interface ChangeGraphPoint {
  value: number;
  date: Date;
}

export interface Change {
  graph: ChangeGraphPoint[];
  title: string;
  type: string;
  changePercentage?: number;
  changeValue?: number;
  startValue?: number;
  endValue?: number;
  formatTemplate: string;
  color: string;
  textColor: string;
}
