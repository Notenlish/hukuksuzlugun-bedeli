import { TypographyP } from "@/components/ui/typography";
export default function Home() {
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
        <TypographyP>
          Hello world! You can edit this page on:{" "}
          <span className=" text-accent bg-neutral-900 px-2 rounded">
            my-app/src/app/page.tsx
          </span>
        </TypographyP>
      </main>
      <footer className="row-start-3 flex gap-[24px] flex-wrap items-center justify-center"></footer>
    </div>
  );
}
