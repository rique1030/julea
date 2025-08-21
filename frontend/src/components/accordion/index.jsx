import styles from "./index.module.css";
import LabeledCheckbox from "@components/labeled_checkbox";
import { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { setWebselection } from "@src/store";

function Accordion({ title, index, accordionIndex, contentKey }) {
   const webselection = useSelector((state) => state.webselection);
   const dispatch = useDispatch();
   const [contents, setContents] = useState({});
   const [contentHeight, setContentHeight] = useState("0px");
   const [accIndex, setAccIndex] = accordionIndex;
   const [isOpen, setIsOpen] = useState(false);

   const toggleAccordion = () => {
      if (accIndex === index) {
         setAccIndex(-1);
      } else {
         setAccIndex(index);
      }
   };

   const onCheckboxChange = (website, isChecked) => {
      const newWebSelection = {
         ...webselection?.webselection,
         [contentKey]: {
            ...webselection?.webselection?.[contentKey],
            [website]: isChecked,
         },
      };
      console.log(newWebSelection);
      dispatch(setWebselection(newWebSelection));
   };

   useEffect(() => {
      if (!webselection?.webselection?.[contentKey]) {
         return;
      }
      setContents(webselection?.webselection?.[contentKey]);
   }, [webselection]);

   useEffect(() => {
      const content_count = Object.keys(contents).length;
      setContentHeight(`${content_count * 1.5 + 0.2}rem`);
      setIsOpen(index === accIndex);
   }, [accIndex]);

   return (
      <div>
         <button className={styles.AccordionButton} onClick={toggleAccordion}>
            {title}
            <i className={`${styles.AccordionButtonIcon} material-icons`}>
               {isOpen ? "expand_less" : "expand_more"}
            </i>
         </button>
         <div
            style={{
               maxHeight: isOpen ? contentHeight : "0px",
               borderBottom: isOpen
                  ? "5px solid rgb(var(--rp-moon-overlay))"
                  : "none",
               height: contentHeight,
            }}
            className={styles.AccordionContent}
         >
            {Object.entries(contents || {})?.map(([website, isChecked]) => (
               <LabeledCheckbox
                  key={website}
                  label={website}
                  checked={isChecked}
                  onChange={() => onCheckboxChange(website, !isChecked)}
               />
            ))}
         </div>
      </div>
   );
}

export default Accordion;
