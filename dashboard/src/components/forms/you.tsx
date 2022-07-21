import { useCallback, useContext } from "react";
import { HouseholdContext } from "../../contexts/HouseholdContext";
import { FormYourChild } from "./your/FormYourChild";
import { FormYourIncome } from "./your/FormYourIncome";
import { FormYourMentalDisability } from "./your/FormYourMentalDisability";
import { FormYourPhysicalDisability } from "./your/FormYourPhysicalDisability";
import { FormYourSpouse } from "./your/FormYourSpouse";

export const FormYou = () => {
  return (
    <>
      <h3>あなたについて</h3>
      <div className="input-group input-group-lg mb-3">
        <span className="input-group-text">生年月日</span>
        <input name="生年月日" className="form-control" type="date" />
      </div>
      <FormYourIncome />
      <FormYourPhysicalDisability />
      <FormYourMentalDisability />
      <FormYourSpouse />
      <FormYourChild />
    </>
  );
};
