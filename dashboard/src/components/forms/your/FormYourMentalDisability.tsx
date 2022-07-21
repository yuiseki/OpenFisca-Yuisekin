import { useCallback, useContext } from "react";
import { YourselfContext } from "../../../contexts/YourselfContext";

export const FormYourMentalDisability = () => {
  const { yourself, setYourself } = useContext(YourselfContext);

  const onChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const newYourself = Object.assign(yourself, {
      精神障害者保健福祉手帳がある:
        event.currentTarget.value === "true" ? true : false,
    });
    setYourself({...newYourself});
  }, []);

  return (
    <div className="input-group input-group-lg mb-3">
      <div className="form-check-inline">
        <input
          className="btn-check"
          type="radio"
          name="精神障害者保健福祉手帳"
          id="精神障害者保健福祉手帳はない"
          value="false"
          checked={
            yourself.精神障害者保健福祉手帳がある === undefined
              ? false
              : !yourself.精神障害者保健福祉手帳がある
          }
          onChange={onChange}
        />
        <label
          className="btn btn-outline-primary"
          htmlFor="精神障害者保健福祉手帳はない"
        >
          精神障害者保健福祉手帳はない
        </label>
      </div>
      <div className="form-check-inline">
        <input
          className="btn-check"
          type="radio"
          name="精神障害者保健福祉手帳"
          id="精神障害者保健福祉手帳がある"
          value="true"
          checked={
            yourself.精神障害者保健福祉手帳がある === undefined
              ? false
              : yourself.精神障害者保健福祉手帳がある
          }
          onChange={onChange}
        />
        <label
          className="btn btn-outline-primary"
          htmlFor="精神障害者保健福祉手帳がある"
        >
          精神障害者保健福祉手帳がある
        </label>
      </div>
    </div>
  );
};
