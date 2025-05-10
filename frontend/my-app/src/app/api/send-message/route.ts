import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  const data = await req.json();

  console.log(process.env.CONTACT_WEBHOOK, data["msg"]);

  const response = await fetch(process.env.CONTACT_WEBHOOK as string, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ content: data["msg"] }),
  });

  if (response.ok) return new NextResponse("successful.", { status: 200 });
  return new NextResponse("failed.", { status: 500 });
}
