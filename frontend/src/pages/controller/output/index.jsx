import styles from "./index.module.css";
import LabeledCheckbox from "@components/labeled_checkbox";
import { useState, useRef } from "react";
import { useSelector } from "react-redux";
import expandIcon from "@assets/icons/expand.png";
import collapseIcon from "@assets/icons/collapse.png";


const LinkTitleLength = 30;

function OutputPanel() {
   const [leaveBrowserOpen, setLeaveBrowserOpen] = useState(false);
   const [isFullscreen, setIsFullscreen] = useState(false);

   const outputRef = useRef(null);
   const originalPositionRef = useRef(null);

   const toggleFullscreen = () => {
      const element = outputRef?.current;
      const animation_speed = 0.1
      if (!element) return;

      if (isFullscreen) {
         setIsFullscreen(false);

         const originalPos = originalPositionRef.current;
         if (!originalPos) return;

         element.style.transition = `all ${animation_speed}s ease-in-out`;
         element.style.top = `${originalPos.top}px`;
         element.style.left = `${originalPos.left}px`;
         element.style.width = `${originalPos.width}px`;
         element.style.height = `${originalPos.height}px`;
         element.style.maxWidth = originalPos.maxWidth;
         element.style.maxHeight = originalPos.maxHeight;
         element.style.borderRadius = originalPos.borderRadius;
         element.style.boxShadow = originalPos.boxShadow;

         setTimeout(() => {
            element.style.position = "relative";
            element.style.top = "";
            element.style.left = "";
            element.style.width = "";
            element.style.height = "";
            element.style.maxWidth = '';
            element.style.maxHeight = '';
            element.style.borderRadius = '';
            element.style.boxShadow = '';
            element.style.zIndex = '';
            element.style.transition = "";
            element.classList.remove(styles.FullScreen);

            originalPositionRef.current = null;
         }, animation_speed * 1000);
      } else {
         setIsFullscreen(true);

         const first = element.getBoundingClientRect();
         const computeStyle = window.getComputedStyle(element);

         originalPositionRef.current = {
            top: first.top,
            left: first.left,
            width: first.width,
            height: first.height,
            maxWidth: computeStyle.maxWidth,
            maxHeight: computeStyle.maxHeight,
            borderRadius: computeStyle.borderRadius,
            boxShadow: computeStyle.boxShadow,
         };

         element.style.position = "fixed";
         element.style.top = `${first.top}px`;
         element.style.left = `${first.left}px`;
         element.style.width = `${first.width}px`;
         element.style.height = `${first.height}px`;
         element.style.transition = '';
         element.style.zIndex = '999';

         void element.offsetWidth;
         element.style.transition = `all ${animation_speed}s ease-in-out`;
         element.style.top = "5vh";
         element.style.left = "5vw";
         element.style.width = "90vw";
         element.style.height = "90vh";
         element.style.maxWidth = 'none';
         element.style.maxHeight = 'none';
         element.style.borderRadius = '0.2rem';
         element.style.boxShadow = '0 0 20px 5px rgba(0, 0, 0, 0.5)';

         element.classList.add(styles.FullScreen);

         setTimeout(() => {
            outputRef.current.style.transition = "";
         }, animation_speed * 1000);
      }

   }

   const output = useSelector((state) => state.output.output);

   return (
      <div className={`Card ${styles.Output}`}>
         <h4 className={styles.SectionTitle}>Output</h4>
         <LabeledCheckbox
            label="Leave browser open"
            checked={leaveBrowserOpen}
            onChange={() => setLeaveBrowserOpen(!leaveBrowserOpen)}
         />
         <div className={`${styles.OutputContainer}`} ref={outputRef}>
            <button onClick={toggleFullscreen} className={styles.FullScreenButton} >
               {isFullscreen ? <img src={collapseIcon} alt="collapse" /> : <img src={expandIcon} alt="expand" />}
            </button>
            {Object.entries(output, {}).map(([key, value]) => (
               <div key={key}>
                  <h5 className={styles.SearchQuery}>{`" ${key.toLowerCase()} "`}</h5>
                  <BrowserList browsers={value} />
               </div>
            ))}
         </div>
      </div>
   );
}

function BrowserList({ browsers }) {
   return (
      <ul>
         {Object.entries(browsers)
            .map(([browser, searches]) => (
               <li key={browser}>
                  <div className={styles.BrowserContainer} >
                     <h5 className={styles.BrowserTitle}>{browser}</h5>
                     <ResultList searches={searches} />
                  </div>
               </li>
            ))}
      </ul>
   );
}


function ResultList({ searches }) {
   // document.addEventListener('click', (e) => {
   //    const a = e.target.closest('a');
   //    if (a && a.href) {
   //       e.preventDefault();
   //       window.pywebview.api.open_in_browser(a.href);
   //    }
   // });
   const on_link_click = async (link) => {
      return await window.pywebview.api.open_in_browser(link);
   }
   return (
      <div>
         <ol>
            {searches.results
               .slice(0, 5)
               .map((result) => (
                  <li key={result.link} target="_blank" rel="noopener noreferrer">
                     <button onClick={() => on_link_click(result.link)}>
                        {result.title}</button> </li>
               ))}
         </ol>
      </div>
   )
}

export default OutputPanel;
