import { useCallback, useContext } from "react";
import { HouseholdContext } from "../../../contexts/HouseholdContext";

export const FormYourIncome = () => {
  const yearMonth = `${new Date().getFullYear()}-${new Date().getMonth()}`;
  const { household, setHousehold } = useContext(HouseholdContext);

  const onChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const newHousehold = {
      ...household,
      世帯員: {
        あなた: {
          所得: {
            [yearMonth]: event.currentTarget.value,
          },
        },
      },
    };
    setHousehold(newHousehold);
  }, []);

  return (
    <div className="input-group input-group-lg mb-3">
      <span className="input-group-text">年収</span>
      <input
        name="年収"
        className="form-control"
        type="number"
        value={household.世帯員.あなた.所得[yearMonth]}
        onChange={onChange}
      />
      <span className="input-group-text">万円</span>
    </div>
  );
};
