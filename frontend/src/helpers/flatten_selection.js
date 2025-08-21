export default function FlattenSelection(selection) {
   return Object.entries(selection).flatMap(([_, inner]) =>
      Object.entries(inner)
         .filter(([_, value]) => value === true)
         .reduce((acc, [key, _]) => { 
                 const new_key = key.split(".").slice(0, -1).join(".");
                return [...acc, new_key];
         }, []),
   );
}
