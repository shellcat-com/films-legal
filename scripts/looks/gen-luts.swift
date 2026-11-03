import Foundation
import ImageIO
import CoreGraphics
import UniformTypeIdentifiers

let outDir = CommandLine.arguments[1]
let dim = Int(CommandLine.arguments[2]) ?? 33
var meta: [String: Any] = [:]
for id in FilmLookLibrary.builtInIDs {
    guard let look = FilmLookLibrary.look(for: id) else { continue }
    let cube = FilmLookCompilerLite.compile(look, dim: dim)
    // strip: width dim*dim (blue slices left→right, red within slice), height dim (green)
    let w = dim * dim, h = dim
    var px = [UInt8](repeating: 255, count: w * h * 4)
    for b in 0..<dim { for g in 0..<dim { for r in 0..<dim {
        let src = ((b * dim + g) * dim + r) * 3
        let x = b * dim + r, y = g
        let o = (y * w + x) * 4
        px[o] = cube[src]; px[o+1] = cube[src+1]; px[o+2] = cube[src+2]; px[o+3] = 255
    } } }
    let cs = CGColorSpace(name: CGColorSpace.sRGB)!
    let ctx = CGContext(data: &px, width: w, height: h, bitsPerComponent: 8, bytesPerRow: w*4, space: cs, bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
    let img = ctx.makeImage()!
    let url = URL(fileURLWithPath: "\(outDir)/\(id).png")
    let dst = CGImageDestinationCreateWithURL(url as CFURL, UTType.png.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(dst, img, nil); CGImageDestinationFinalize(dst)
    var m: [String: Any] = [:]
    if let st = LookStageLibrary.stages(for: id) {
        if let v = st.vignette { m["vignette"] = [v.stops, v.power, v.elliptical] }
        if let gr = st.grain { m["grain"] = [gr.cellsAcross, gr.amount, gr.chroma, gr.density ? 1 : 0] }
        if st.halation != nil { m["halation"] = 1 }
        if st.leak != nil { m["leak"] = 1 }
    }
    meta[id] = m
}
let data = try! JSONSerialization.data(withJSONObject: meta, options: [.sortedKeys, .prettyPrinted])
try! data.write(to: URL(fileURLWithPath: "\(outDir)/stages.json"))

enum FilmLookCompilerLite {
    static func compile(_ look: FilmLook, dim: Int) -> [UInt8] {
        let ev = FilmLookEvaluator(look, gamut: .sRGB)
        let den = Double(dim - 1)
        var out = [UInt8](repeating: 0, count: dim*dim*dim*3)
        for b in 0..<dim { for g in 0..<dim { for r in 0..<dim {
            let v = ev.apply(SIMD3(Double(r), Double(g), Double(b)) / den)
            let o = ((b * dim + g) * dim + r) * 3
            out[o] = UInt8((min(max(v.x,0),1) * 255).rounded()); out[o+1] = UInt8((min(max(v.y,0),1) * 255).rounded()); out[o+2] = UInt8((min(max(v.z,0),1) * 255).rounded())
        } } }
        return out
    }
}
