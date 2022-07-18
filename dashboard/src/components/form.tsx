import { useContext, useEffect } from "react";
import { HouseholdContext } from "../contexts/HouseholdContext";
import { useCalculate } from "../hooks/calculate";

export const OpenFiscaForm = () => {
  const result = useCalculate();
  const { household, setHousehold } = useContext(HouseholdContext);

  return (
    <div>
      <h2>試す</h2>
      <form>
        <div className="input-group input-group-lg mb-3">
          <span className="input-group-text">生年月日</span>
          <input name="生年月日" className="form-control" type="date" />
        </div>
        <div className="input-group input-group-lg mb-3">
          <span className="input-group-text">年収</span>
          <input name="年収" className="form-control" type="number" />
          <span className="input-group-text">万円</span>
        </div>
        <div className="input-group input-group-lg mb-3">
          <div className="form-check-inline">
            <input
              className="btn-check"
              type="radio"
              name="配偶者"
              id="配偶者はいない"
              value="false"
            />
            <label className="btn btn-outline-primary" htmlFor="配偶者はいない">
              配偶者はいない
            </label>
          </div>
          <div className="form-check-inline">
            <input
              className="btn-check"
              type="radio"
              name="配偶者"
              id="配偶者がいる"
              value="true"
            />
            <label className="btn btn-outline-primary" htmlFor="配偶者がいる">
              配偶者がいる
            </label>
          </div>
        </div>
        <div className="input-group input-group-lg mb-3">
          <div className="form-check-inline">
            <input
              className="btn-check"
              type="radio"
              name="子ども"
              id="子どもはいない"
              value="false"
            />
            <label className="btn btn-outline-primary" htmlFor="子どもはいない">
              子どもはいない
            </label>
          </div>
          <div className="form-check-inline">
            <input
              className="btn-check"
              type="radio"
              name="子ども"
              id="子どもがいる"
              value="true"
            />
            <label className="btn btn-outline-primary" htmlFor="子どもがいる">
              子どもがいる
            </label>
          </div>
        </div>
      </form>
      <h2>結果</h2>
      {result && <pre>{JSON.stringify(result.世帯.世帯1, null, 2)}</pre>}
    </div>
  );
};
