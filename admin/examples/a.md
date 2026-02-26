    const computeNextIds = obj => {
      const res = {};
      Object.keys(obj).forEach(dir => {
        const arr = obj[dir] || [];
        res[dir] = (arr.reduce((m,t)=>Math.max(m,t.id||0),0))+1;
      });
      return res;
    };


inside  the const loadLS:
```
      nextIdByDirectory = computeNextIds(tracksByDirectory);
```    
