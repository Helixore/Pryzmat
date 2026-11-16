import { apiGet } from "../API/auth/client";

export function GetStudents(){
  let data = apiGet("/student/");
  console.log(data);
}

export default function Students() {
  GetStudents();
  return (
    <div>
      <h1>Uczniowie</h1>
      {/* tu docelowo lista z API */}
    </div>
  );
}