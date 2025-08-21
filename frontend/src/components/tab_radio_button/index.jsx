import styles from "./index.module.css";

function TabRadioButton({ labels, valueSelectorState }) {
   const [value, setValue] = valueSelectorState;
   return (
      <div className={styles.TabRadioButton}>
         {labels?.map((label, index) => (
            <button
               key={index}
               style={{
                  "--button-color":
                     value?.toLowerCase() == label?.toLowerCase()
                        ? "var(--rp-moon-foam)"
                        : "",
               }}
               onClick={() => setValue(label.toLowerCase())}
            >
               {label}
            </button>
         ))}
      </div>
   );
}

export default TabRadioButton;
