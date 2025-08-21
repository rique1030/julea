import styles from "./index.module.css";

function LabeledCheckbox({ label, checked, onChange }) {
   return (
      <label className={styles.LabeledCheckbox}>
         <i
            style={{ color: checked ? "rgb(var(--rp-moon-love))" : "" }}
            className={`material-icons-outlined`}
         >
            check
         </i>
         <input
            type="checkbox"
            checked={checked}
            onChange={(e) => {
               if (onChange) {
                  onChange(e.target.checked);
               }
            }}
         />
         {label}
      </label>
   );
}

export default LabeledCheckbox;
