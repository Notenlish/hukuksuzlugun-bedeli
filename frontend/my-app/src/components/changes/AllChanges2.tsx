import { Change } from "@/types";
import ChangeComponent from "./change";

export default function AllChanges2({changes}:{changes:Change[]}) {
  return changes.map((e,i) => <ChangeComponent key={i} id={i} change={e}></ChangeComponent>)
}
