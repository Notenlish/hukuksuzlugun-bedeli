import { NextResponse } from "next/server";

let API_BASE_URL = process.env.API_URL;
if (process.env.NODE_ENV == "development") {
  API_BASE_URL = "http://127.0.0.1:8000";
}

if (!API_BASE_URL) {
  throw new Error("API_BASE_URL is undefined.");
}

let cacheTime = 3600;   // 1 hour
if (process.env.NODE_ENV == "development") {
  cacheTime = 1
}

export async function GET() {
  try {
    if (!API_BASE_URL) {
      throw new Error("EXTERNAL_API_URL environment variable is not set.");
    }
    if (!process.env.API_KEY) {
      throw new Error("API_KEY environment variable is not set.");
    }

    console.log("SENDING REQUEST TO BACKEND");
    const apiRes = await fetch(API_BASE_URL + "/get-change", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-API-Key": process.env.API_KEY,
      },
      next: { revalidate: cacheTime }, // 1 hour
    });

    console.log("SENT REQUEST TO BACKEND, HOPE IT WAS SUCCESSFUL");
    if (!apiRes.ok) {
      const errorBody = await apiRes.text(); // Read the error response body
      console.log(apiRes);
      console.error(
        `Failed to fetch from external API: ${apiRes.status} ${apiRes.statusText} - ${errorBody}`,
      );
      return NextResponse.json(
        { error: `Failed to retrieve data: ${apiRes.statusText}` },
        { status: apiRes.status },
      );
    }

    console.log("LETS GOO TIME TO MAKE DATA JSON");
    const data = await apiRes.json();
    console.log(data)
    return NextResponse.json(data);
  } catch (e) {
    console.error("Error in API route:", e);
    return NextResponse.json(
      { error: "Internal Server Error" },
      { status: 500 },
    );
  }
}
