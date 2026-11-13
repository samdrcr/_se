function logInfo(message) {
    console.log(`[INFO] 📘 ${message}`);
}
function logSuccess(message) {
    console.log(`[SUCCESS] 🟩 ${message}`);
}
function logError(message) {
    console.error(`[ERROR] 🟥 ${message}`);
}
module.exports = { logInfo, logSuccess, logError };
