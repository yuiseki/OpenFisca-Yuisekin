import { useContext, useEffect, useState } from "react";
import { HouseholdContext } from "../contexts/HouseholdContext";

export const useCalculate = () => {
  const [result, setResult] = useState<any>();
  const { household } = useContext(HouseholdContext);

  console.log(household);

  useEffect(() => {
    if (!household) {
      return;
    }
    (async () => {
      const newResultRes = await fetch("http://localhost:50000/calculate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(household),
      });
      const newResultJson = await newResultRes.json();
      delete newResultJson.世帯.世帯1.保護者一覧;
      delete newResultJson.世帯.世帯1.児童一覧;
      setResult(newResultJson);
    })();
  }, [household]);

  return result;
};
