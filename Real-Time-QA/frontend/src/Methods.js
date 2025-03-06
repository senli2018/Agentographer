export const SpellingCharacters = (obj) => {
    return Object.keys(obj)
        .filter(key => obj[key] !== null && obj[key] !== undefined && obj[key] !== '')
        .map(key => `${key}=${obj[key]}`)
        .join('&');
};