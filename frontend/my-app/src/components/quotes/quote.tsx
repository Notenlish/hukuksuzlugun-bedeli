/** eslint-disable @typescript-eslint/no-unused-vars */
// import quote from "quote.svg";
import Image from "next/image";
import { TypographyP } from "@/components/ui/typography";
import Link from "next/link";
import { QuoteData } from "@/types";

export default function Quote({ quoteData }: { quoteData: QuoteData }) {
  const q = quoteData;
  return (
    <div className="border p-4 rounded bg-red-200">
      <div className="flex gap-4 max-w-256">
        <div className="relative putquotes grid content-center">
          <div className="p-2 text-center w-180 pt-8">
            <TypographyP>{q.text}</TypographyP>
          </div>
        </div>
        <div className="w-96 flex flex-col gap-2 content-center items-center">
          <Image
            className="rounded"
            alt={q.author}
            src={q.image}
            width={640}
            height={360}
          ></Image>
        </div>
      </div>
      <div className="flex flex-col mt-2 items-end">
        <div className="text-center w-fit">{q.author}</div>
        <Link
          className="underline w-fit"
          href="https://10haber.net/ekonomi/iso-baskani-bahcivan-hizmet-enflasyonunun-bedelini-sanayici-oduyor-606543/"
        >
          Kaynak
        </Link>
      </div>
    </div>
  );
}
