import { Change } from "@/types";
import ChangeComponent from "./change";
import { Skeleton } from "../ui/skeleton";

export default function AllChanges2({ changes, loaded }: { changes: Change[]; loaded:boolean}) {
  return <>
    {loaded ? changes.map((e,i) => <ChangeComponent key={i} id={i} change={e}></ChangeComponent>) : <Skeleton className="h-192 w-full"></Skeleton> }
  </>
}
