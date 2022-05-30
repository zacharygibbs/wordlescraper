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
