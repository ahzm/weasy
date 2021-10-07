```js
<Couples
  key={"unique_id_couple1" + "unique_id_couple2"}
  c1={"description couple 1"}
  c2={"description couple 2"}
  couple={[{desc:"Couple 1", id:"id couple 1"},{desc:"couple 2", id: "id couple 1", }]}
  deleteCouple={() => {
    let newCouples = [...couples];
    newCouples.filter((c, i) => {
      if (c[1] === couple[1] && c[0] === couple[0]) {
        if (i > -1) {
          newCouples.splice(i, 1);
        }
        return c;
      }
      return false;
    });
    setCouples(newCouples);
  }}
/>
```
