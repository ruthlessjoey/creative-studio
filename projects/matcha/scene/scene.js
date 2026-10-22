// Matcha iced latte: real-time 3D scene (three.js r186). Deterministic: everything is a function of time t,
// so the same module drives the live website and the frame-by-frame video render.
import * as THREE from 'three';

const NOISE = `
float h31(vec3 p){p=fract(p*.3183099+.1);p*=17.;return fract(p.x*p.y*p.z*(p.x+p.y+p.z));}
float vn(vec3 x){vec3 i=floor(x),f=fract(x);f=f*f*(3.-2.*f);
 return mix(mix(mix(h31(i),h31(i+vec3(1,0,0)),f.x),mix(h31(i+vec3(0,1,0)),h31(i+vec3(1,1,0)),f.x),f.y),
            mix(mix(h31(i+vec3(0,0,1)),h31(i+vec3(1,0,1)),f.x),mix(h31(i+vec3(0,1,1)),h31(i+vec3(1,1,1)),f.x),f.y),f.z);}
float fbm(vec3 p){float a=.5,s=0.;for(int i=0;i<4;i++){s+=a*vn(p);p*=2.02;a*=.5;}return s;}
`;
const LIQ_VS = `varying vec3 vP,vN,vV;void main(){vP=position;vec4 mv=modelViewMatrix*vec4(position,1.);vN=normalMatrix*normal;vV=-mv.xyz;gl_Position=projectionMatrix*mv;}`;
const LIQ_FS = `
uniform float uTime,uFill,uMode;varying vec3 vP,vN,vV;
${NOISE}
void main(){
 if(uMode<.5&&vP.y>uFill)discard;
 float h=clamp((vP.y-.22)/max(uFill-.22,.001),0.,1.);
 vec3 q=vec3(vP.x,h*2.,vP.z);
 float a=h*4.+uTime*.25;mat2 R=mat2(cos(a),-sin(a),sin(a),cos(a));q.xz=R*q.xz;
 float n=fbm(q*2.+vec3(0.,uTime*.12,0.)),n2=fbm(q*5.-uTime*.1);
 vec3 milk=vec3(.94,.91,.80),deep=vec3(.27,.40,.10),lite=vec3(.56,.70,.22),col;
 if(uMode<.5){
  float e=h+(n-.5)*.6+(n2-.5)*.14;float m=smoothstep(.30,.58,e);
  float s=sin((q.x*3.+q.z*2.+n*6.)*2.+uTime*.4);
  vec3 mat=mix(deep,lite,smoothstep(.2,.8,n2+s*.1+h*.35));
  col=mix(milk,mat,m);
 }else{
  vec2 p=vP.xz;float b=smoothstep(.72,.9,vn(vec3(p*34.,uTime*.05)));
  float sw=fbm(vec3(p*2.2,uTime*.1));
  col=mix(vec3(.40,.56,.14),vec3(.66,.78,.30),sw);col=mix(col,milk,smoothstep(.62,.82,fbm(vec3(p*3.5+3.,uTime*.08)))*.55);
  col+=b*.12;
 }
 vec3 N=normalize(vN),V=normalize(vV);float f=pow(1.-abs(dot(N,V)),2.5);
 float d=.62+.38*dot(N,normalize(vec3(.4,.6,.7)));
 col*=d;col=mix(col,col*1.25+vec3(.05,.08,.02),f*.7);
 col=pow(col,vec3(2.2));
 gl_FragColor=vec4(col,1.);
 #include <tonemapping_fragment>
 #include <colorspace_fragment>
}`;

function innerR(y){return .52+(y-.22)/(2.3-.22)*.12;}
function glassProfile(){
  const P=[[0,0],[.50,0],[.56,.035],[.575,.12],[.70,2.3],[.64,2.3],[.64,2.29],[.595,.26],[.52,.22],[0,.22]];
  return P.map(([r,y])=>new THREE.Vector2(r,y));
}
function liquidProfile(){
  const P=[[0,.221],[.515,.221],[.585,.27],[.635,2.29]];
  return P.map(([r,y])=>new THREE.Vector2(r,y));
}
function roundedCube(s,r){
  const g=new THREE.BoxGeometry(s,s,s,8,8,8),p=g.attributes.position,h=s/2-r,v=new THREE.Vector3(),c=new THREE.Vector3();
  for(let i=0;i<p.count;i++){v.fromBufferAttribute(p,i);c.set(THREE.MathUtils.clamp(v.x,-h,h),THREE.MathUtils.clamp(v.y,-h,h),THREE.MathUtils.clamp(v.z,-h,h));
    v.sub(c).normalize().multiplyScalar(r).add(c);p.setXYZ(i,v.x,v.y,v.z);}
  g.computeVertexNormals();return g;
}
function mulberry(a){return()=>{a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}
const clamp01=x=>Math.min(1,Math.max(0,x)), sstep=(a,b,x)=>{x=clamp01((x-a)/(b-a));return x*x*(3-2*x);};
const easeOut=x=>1-Math.pow(1-clamp01(x),3), easeIn=x=>{x=clamp01(x);return x*x;};

export async function createScene({canvas,width,height,pixelRatio=1,word='MATCHA',rows=3,fontCss='900 100px AB',samples=4}){
  const renderer=new THREE.WebGLRenderer({canvas,antialias:true,preserveDrawingBuffer:true,powerPreference:'high-performance'});
  renderer.setPixelRatio(pixelRatio);renderer.setSize(width,height,false);
  renderer.toneMapping=THREE.NeutralToneMapping;renderer.toneMappingExposure=1.0;renderer.outputColorSpace=THREE.SRGBColorSpace;
  const scene=new THREE.Scene();
  const camera=new THREE.PerspectiveCamera(28,width/height,.1,60);

  // environment: studio softboxes (reflected in glass and ice)
  const envS=new THREE.Scene();
  envS.add(new THREE.Mesh(new THREE.SphereGeometry(20,32,16),new THREE.MeshBasicMaterial({color:new THREE.Color(.62,.60,.54),side:THREE.BackSide})));
  const box=(w,h,x,y,z,i,ry=0)=>{const m=new THREE.Mesh(new THREE.PlaneGeometry(w,h),new THREE.MeshBasicMaterial({color:new THREE.Color(i,i,i*.96),side:THREE.DoubleSide}));m.position.set(x,y,z);m.lookAt(0,1.2,0);m.rotation.z+=ry;envS.add(m);};
  box(1.4,9,-6,2,3,9);box(.7,9,6.5,2,2,6);box(8,8,0,9,1,4);box(3,6,0,2,-8,5);box(5,.8,0,.2,8,2.5);
  const pm=new THREE.PMREMGenerator(renderer);scene.environment=pm.fromScene(envS,.02).texture;pm.dispose();

  // backdrop: giant stacked word (refracted by the glass), drawn from the page's embedded font
  await document.fonts.load('100px AB');
  const bd={cv:document.createElement('canvas')};const bt=new THREE.CanvasTexture(bd.cv);bt.colorSpace=THREE.SRGBColorSpace;bt.anisotropy=8;
  const backMat=new THREE.MeshBasicMaterial({map:bt,toneMapped:false});const back=new THREE.Mesh(new THREE.PlaneGeometry(1,1),backMat);back.position.set(0,1.3,-1.7);scene.add(back);
  const BG={w:0,h:0,fs:0,tw:0,pad:0,capH:0,gap:0,y0:0,ready:false};
  const rowCols=['#2F3A14','#556B24','#8FA05A','#B7C08C','#D5D9B8'];
  function setupBackdrop(w,h){
    const cv=bd.cv;cv.width=Math.min(2048,Math.round(w));cv.height=Math.round(cv.width*h/w);const c=cv.getContext('2d');
    const tw=cv.width/1.55*.9;c.font=fontCss;const m=c.measureText(word).width;const fs=100*tw/m;
    Object.assign(BG,{tw,pad:(cv.width-tw)/2,fs,capH:fs*.72,ready:true});BG.gap=BG.capH*.07;BG.y0=(cv.height-(rows*BG.capH+(rows-1)*BG.gap))/2+BG.capH;lastBg=-1;
  }
  let lastBg=-1;
  function drawBackdrop(t){
    if(!BG.ready)return;const key=Math.round(t*60);if(key===lastBg)return;lastBg=key;
    const cv=bd.cv,c=cv.getContext('2d');c.fillStyle='#E9E7D8';c.fillRect(0,0,cv.width,cv.height);
    c.font=fontCss.replace('100px',BG.fs+'px');c.textBaseline='alphabetic';
    for(let i=0;i<rows;i++){
      const dir=i%2?1:-1,enter=(1-easeOut((t-.1-i*.12)/1.2))*dir*cv.width*.95,sway=Math.sin(t*.35+i*1.3)*cv.width*.012*(i+1)*.6;
      c.fillStyle=rowCols[Math.min(i,rowCols.length-1)];
      c.fillText(word,BG.pad+enter+sway,BG.y0+i*(BG.capH+BG.gap));
    }
    bt.needsUpdate=true;
  }
  // decals: contact shadow + green caustic glow
  const mkRad=(inner,outer,sz=256)=>{const cv=document.createElement('canvas');cv.width=cv.height=sz;const c=cv.getContext('2d'),g=c.createRadialGradient(sz/2,sz/2,0,sz/2,sz/2,sz/2);g.addColorStop(0,inner);g.addColorStop(1,outer);c.fillStyle=g;c.fillRect(0,0,sz,sz);const t=new THREE.CanvasTexture(cv);t.colorSpace=THREE.SRGBColorSpace;return t;};
  const shadow=new THREE.Mesh(new THREE.PlaneGeometry(2.5,2.5),new THREE.MeshBasicMaterial({map:mkRad('rgba(20,30,8,.5)','rgba(20,30,8,0)'),transparent:true,depthWrite:false}));shadow.rotation.x=-Math.PI/2;shadow.position.y=.002;scene.add(shadow);
  const glow=new THREE.Mesh(new THREE.PlaneGeometry(3.6,3.6),new THREE.MeshBasicMaterial({map:mkRad('rgba(120,170,40,.55)','rgba(120,170,40,0)'),transparent:true,depthWrite:false,blending:THREE.MultiplyBlending,premultipliedAlpha:true}));glow.visible=false;

  const root=new THREE.Group();scene.add(root);
  // glass
  const glassMat=new THREE.MeshPhysicalMaterial({color:0xffffff,metalness:0,roughness:.02,transmission:1,thickness:1.1,ior:1.52,envMapIntensity:2.3,specularIntensity:1,clearcoat:0,attenuationColor:new THREE.Color(.86,.97,.86),attenuationDistance:3.2,depthWrite:false});
  const glass=new THREE.Mesh(new THREE.LatheGeometry(glassProfile(),96),glassMat);glass.renderOrder=2;root.add(glass);
  // liquid
  const liqU={uTime:{value:0},uFill:{value:.22},uMode:{value:0}},capU={uTime:liqU.uTime,uFill:{value:.22},uMode:{value:1}};
  const liq=new THREE.Mesh(new THREE.LatheGeometry(liquidProfile(),96),new THREE.ShaderMaterial({uniforms:liqU,vertexShader:LIQ_VS,fragmentShader:LIQ_FS,side:THREE.DoubleSide}));root.add(liq);
  const cap=new THREE.Mesh(new THREE.CircleGeometry(1,96),new THREE.ShaderMaterial({uniforms:capU,vertexShader:LIQ_VS,fragmentShader:LIQ_FS}));cap.rotation.x=-Math.PI/2;root.add(cap);
  // ice (frosted cubes)
  const iceTex=(()=>{const cv=document.createElement('canvas');cv.width=cv.height=256;const c=cv.getContext('2d'),r=mulberry(5);c.fillStyle='#808080';c.fillRect(0,0,256,256);
    for(let i=0;i<60;i++){c.strokeStyle=`rgba(${r()>.5?255:0},${r()>.5?255:0},${r()>.5?255:0},.08)`;c.lineWidth=1+r()*2;c.beginPath();c.moveTo(r()*256,r()*256);c.lineTo(r()*256,r()*256);c.stroke();}
    const t=new THREE.CanvasTexture(cv);t.wrapS=t.wrapT=THREE.RepeatWrapping;return t;})();
  const iceMat=new THREE.MeshPhysicalMaterial({color:0xe4f1e8,roughness:.16,metalness:0,clearcoat:1,clearcoatRoughness:.1,envMapIntensity:1.6,bumpMap:iceTex,bumpScale:1.5,transparent:true,opacity:.62,ior:1.31,specularIntensity:1});
  const ice=[];const rnd=mulberry(21);
  const IC=[[.18,.35,.22,1.0],[-.22,.62,.25,.9],[.05,.9,-.2,1.05],[-.12,1.2,.15,.95],[.24,1.28,-.05,.85]];
  IC.forEach(([x,y,z,s],i)=>{const m=new THREE.Mesh(roundedCube(.42*s,.06),iceMat);m.userData={x,y,z,r:[rnd()*6,rnd()*6,rnd()*6],i};ice.push(m);root.add(m);});
  // straw
  const straw=new THREE.Mesh(new THREE.CylinderGeometry(.05,.05,2.9,24,1,true),new THREE.MeshPhysicalMaterial({color:0x7a9a46,roughness:.45,side:THREE.DoubleSide,envMapIntensity:.8}));
  straw.position.set(.2,1.75,-.1);straw.rotation.set(.04,0,-.12);root.add(straw);
  // pour stream
  const stream=new THREE.Mesh(new THREE.CylinderGeometry(.04,.034,1,20,1,true),new THREE.MeshPhysicalMaterial({color:0x5c7a22,roughness:.12,clearcoat:1,envMapIntensity:1.5,side:THREE.DoubleSide}));stream.visible=false;root.add(stream);
  // condensation droplets
  const DN=150,dr=new THREE.InstancedMesh(new THREE.SphereGeometry(1,14,10),new THREE.MeshPhysicalMaterial({color:0xffffff,roughness:0,transmission:1,thickness:.12,ior:1.33,envMapIntensity:2,transparent:false}),DN);
  const dd=[],dm=new THREE.Object3D(),r2=mulberry(99);
  for(let i=0;i<DN;i++){dd.push({a:(r2()-.5)*Math.PI*2.2,y:.35+r2()*1.8,s:.012+Math.pow(r2(),2.5)*.04,slide:r2()<.07,sp:.02+r2()*.03});}
  root.add(dr);
  // matcha dust
  const PN=260,pg=new THREE.BufferGeometry(),pp=new Float32Array(PN*3),pb=[],r3=mulberry(7);
  for(let i=0;i<PN;i++){pb.push({x:(r3()-.5)*4,y:r3()*3.2,z:(r3()-.5)*2+.4,f:.2+r3()*.5,p:r3()*6.28});}
  pg.setAttribute('position',new THREE.BufferAttribute(pp,3));
  const dust=new THREE.Points(pg,new THREE.PointsMaterial({color:0x7d9a2c,size:.028,transparent:true,opacity:.75,depthWrite:false}));scene.add(dust);

  const cam={az:0,el:.2,dist:7.6,ty:1.3,fov:28,tx:0};
  function layout(w,h){camera.aspect=w/h;camera.updateProjectionMatrix();renderer.setSize(w,h,false);
    const dist=8.2+1.7,vh=2*Math.tan(camera.fov*Math.PI/360)*dist*1.55;back.scale.set(vh*camera.aspect,vh,1);setupBackdrop(2048,2048*h/w);}
  const view={cx:0,cy:0};

  function setCamera(o){Object.assign(cam,o);}
  function update(t){
    liqU.uTime.value=t;drawBackdrop(t);
    // intro choreography
    const iceIn=i=>easeIn((t-.25-i*.14)/.55);                      // ice drops in
    const fill=.22+(1.78-.22)*sstep(.9,3.4,t)*(1-.0);              // pour fills glass
    liqU.uFill.value=fill;capU.uFill.value=fill;
    const rr=innerR(fill)-.004;cap.scale.set(rr,rr,1);cap.position.y=fill+.001;
    const OFF=[.04,.16,-.03,.11,.2];
    ice.forEach(m=>{const u=m.userData,k=iceIn(u.i),fall=(1-k)*2.8;
       const bob=Math.sin(t*.9+u.i*1.7)*.025+Math.sin(t*.5+u.i)*.012,by=fill+OFF[u.i]+bob;
       m.position.set(u.x*1.15,Math.max(by,.35)+fall,u.z*1.1);m.visible=k>0;
       const spin=t*.18+u.i;m.rotation.set(u.r[0]+spin*.3+(1-k)*2,u.r[1]+spin*.2,u.r[2]+spin*.25);});
    // pour stream
    const s0=.8,s1=3.4,on=t>s0&&t<s1+.35;stream.visible=on;
    if(on){const top=3.9,bot=Math.max(fill,.25),len=top-bot,grow=easeOut((t-s0)/.35),shrink=1-easeIn((t-s1)/.35);
      const L=len*grow,w=Math.max(.0001,shrink)*(1+.1*Math.sin(t*14));stream.scale.set(w,L,w);stream.position.set(.02,bot+L/2+ (1-grow)*(len-L)*0 ,.0);
      stream.position.y=top-L/2;}
    // droplets
    for(let i=0;i<DN;i++){const d=dd[i];let y=d.y;if(d.slide)y=d.y-((t*d.sp)%1.2);if(y<.3)y+=1.2;
      const r=.575+(y-.12)/(2.3-.12)*.125+.004,x=Math.sin(d.a)*r,z=Math.cos(d.a)*r;
      dm.position.set(x,y,z);dm.scale.set(d.s,d.s*(d.slide?1.8:1.05),d.s*.6);dm.rotation.y=d.a;dm.updateMatrix();dr.setMatrixAt(i,dm.matrix);}
    dr.instanceMatrix.needsUpdate=true;
    // dust
    for(let i=0;i<PN;i++){const b=pb[i];pp[i*3]=b.x+Math.sin(t*b.f+b.p)*.12;pp[i*3+1]=((b.y+t*.05*b.f*3)%3.4);pp[i*3+2]=b.z+Math.cos(t*b.f*.8+b.p)*.1;}
    pg.attributes.position.needsUpdate=true;
    // camera
    const a=cam.az,e=cam.el,d=cam.dist;camera.fov=cam.fov;camera.updateProjectionMatrix();
    camera.position.set(cam.tx+Math.sin(a)*Math.cos(e)*d,cam.ty+Math.sin(e)*d,Math.cos(a)*Math.cos(e)*d);camera.lookAt(cam.tx,cam.ty,0);
    // keep the backdrop facing the camera & behind the glass
    back.position.set(0,cam.ty,-1.7);back.rotation.y=a*.0;
    root.rotation.y=0;
  }
  function render(t){update(t);renderer.render(scene,camera);}
  layout(width,height);
  return {BG,bd,render,setCamera,cam,layout,renderer,scene,camera,dispose(){renderer.dispose();},introEnd:3.8};
}
