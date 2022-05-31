export const dotprod = (df, var1, var2) => {
    return df[var1].reduce(
        (total, curval, curind) => {
            return total + df[var1][curind]*df[var2][curind]
        }, 0
    )
}

export const sum = (arr) => {
    return arr.reduce(function (a, b) {
        return a + b;
    }, 0);
}

export const setSelectedValue = (selectObj, valueToSet) => {
    for (var i = 0; i < selectObj.options.length; i++) {
        if (selectObj.options[i].text== valueToSet) {
            selectObj.options[i].selected = true;
            return;
        }
    }
}

export const calcAvg = (pct1, pct2, pct3, pct4, pct5, pct6, pctx) => {
    return (pct1 * 1 + pct2 * 2 + pct3 * 3 + pct4 * 4 + pct5 * 5 + pct6 * 6 + pctx * 7) / 100
}