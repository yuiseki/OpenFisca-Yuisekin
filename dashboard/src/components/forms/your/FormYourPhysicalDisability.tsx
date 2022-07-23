import { useCallback, useContext } from "react";
import { YourselfContext } from "../../../contexts/YourselfContext";

export const FormYourPhysicalDisability = () => {
  const { yourself, setYourself } = useContext(YourselfContext);

  const onChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const newYourself = Object.assign(yourself, {
      身体障害者手帳がある: event.currentTarget.value === "true" ? true : false,
    });
    setYourself({...newYourself});
  }, []);

  return (
    <div className="input-group input-group-lg mb-3">
      <div className="form-check-inline">
        <input
          className="btn-check"
          type="radio"
          name="身体障害者手帳"
          id="身体障害者手帳はない"
          value="false"
          checked={
            yourself.身体障害者手帳がある === undefined
              ? false
              : !yourself.身体障害者手帳がある
          }
          onChange={onChange}
        />
        <label
          className="btn btn-outline-primary"
          htmlFor="身体障害者手帳はない"
        >
          身体障害者手帳はない
        </label>
      </div>
      <div className="form-check-inline">
        <input
          className="btn-check"
          type="radio"
          name="身体障害者手帳"
          id="身体障害者手帳がある"
          value="true"
          checked={
            yourself.身体障害者手帳がある === undefined
              ? false
              : yourself.身体障害者手帳がある
          }
          onChange={onChange}
        />
        <label
          className="btn btn-outline-primary"
          htmlFor="身体障害者手帳がある"
        >
          身体障害者手帳がある
        </label>
      </div>
    </div>
  );
};
