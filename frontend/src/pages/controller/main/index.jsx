import styles from "./index.module.css";
import Accordion from "@components/accordion";
import TabRadioButton from "@components/tab_radio_button";
import { useState, useEffect, useMemo, useRef } from "react";
import { useSelector, useDispatch } from "react-redux";
import { setWebselection, setSearchmethod } from "@src/store";

function MainPanel() {
   return (
      <div className={`Card ${styles.ControllerConfig}`}>
         <WebsiteSelectionSection />
         <SearchMethodSection />
      </div>
   );
}

function WebsiteSelectionSection() {
   const dispatch = useDispatch();
   const accordionIndex = useState(-1);

   return (
      <div className={styles.WebsiteSelectionContainer}>
         <h4 className={styles.SectionTitle}>Website Selection</h4>
         <Accordion
            title="Chinese Websites"
            contentKey="chinese"
            index={0}
            accordionIndex={accordionIndex}
         />
         <Accordion
            title="Euro/American Websites"
            contentKey="euroamerican"
            index={1}
            accordionIndex={accordionIndex}
         />
         <Accordion
            title="Shared Websites"
            contentKey="shared"
            index={2}
            accordionIndex={accordionIndex}
         />
      </div>
   );
}

function SearchMethodSection() {
   // const [searchMethod, setSearchMethod] = useState("single");
   const searchMethod = useSelector((state) => state.searchmethod.searchmethod);
   const dispatch = useDispatch();

   const setSearchMethod = (method) => {
      dispatch(setSearchmethod({ searchmethod: method }));
   };

   const handleFileInput = (e) => {
      const file = e.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = (e) => {
         const content = e.target.result;
         const lines = content.split("\n");
         dispatch(
            setSearchmethod({
               ...searchMethod,
               bulk: lines,
            }),
         );
      };

      reader.readAsText(file);
   };

   const onSingleChange = (e) => {
      dispatch(
         setSearchmethod({
            ...searchMethod,
            single: e.target.value,
         }),
      );
   };

   return (
      <div className={styles.SearchMethodContainer}>
         <h4 className={styles.SectionTitle}>Search Method</h4>
         <TabRadioButton
            labels={["Bulk", "Single"]}
            valueSelectorState={[searchMethod?.searchmethod, setSearchMethod]}
         />
         {searchMethod.searchmethod == "bulk" && (
            <input type="file" accept=".txt" onChange={handleFileInput} />
         )}
         {searchMethod.searchmethod == "single" && (
            <input
               type="text"
               placeholder="Company Name"
               onChange={onSingleChange}
            />
         )}
      </div>
   );
}

export default MainPanel;
