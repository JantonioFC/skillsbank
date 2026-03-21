const fs = require("fs");
const path = require("path");

function isPathInside(basePath, candidatePath) {
  const base = fs.existsSync(basePath) ? getRealPath(basePath) : path.resolve(basePath);
  const candidate = path.resolve(candidatePath);
  const relative = path.relative(base, candidate);
  return relative === "" || (!relative.startsWith("..") && !path.isAbsolute(relative));
}

function getRealPath(targetPath) {
  try {
    if (typeof fs.realpathSync.native === "function") {
      return fs.realpathSync.native(targetPath);
    }
    return fs.realpathSync(targetPath);
  } catch (err) {
    if (err.code === "ENOENT") return null;
    throw err;
  }
}

function resolveSafeRealPath(rootPath, targetPath) {
  const realPath = getRealPath(targetPath);
  if (!realPath) return null;
  return isPathInside(rootPath, realPath) ? realPath : null;
}

module.exports = {
  getRealPath,
  isPathInside,
  resolveSafeRealPath,
};
