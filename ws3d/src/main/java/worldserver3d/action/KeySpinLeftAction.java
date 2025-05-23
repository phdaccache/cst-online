/*****************************************************************************
 * Copyright 2007-2015 DCA-FEEC-UNICAMP
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *  http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * Contributors:
 *    Patricia Rocha de Toro, Elisa Calhau de Castro, Ricardo Ribeiro Gudwin
 *****************************************************************************/

package worldserver3d.action;

/**
 *
 * @author gudwin
 */
import com.jme.input.action.InputActionEvent;
import com.jme.input.action.KeyInputAction;
import com.jme.math.Matrix3f;
import com.jme.math.Ray;
import com.jme.math.Vector2f;
import com.jme.math.Vector3f;
import com.jme.renderer.Camera;
import com.jme.system.DisplaySystem;

/**
 * <code>KeyRotateLeftAction</code> performs the action of rotating a camera a
 * certain angle. This angle is determined by the speed at which the camera can
 * turn and the time between frames.
 * 
 * @author Mark Powell
 * @version $Id: KeyRotateLeftAction.java,v 1.16 2006/09/29 22:30:17 nca Exp $
 */
public class KeySpinLeftAction extends KeyInputAction {
    //the camera to manipulate
    private Camera camera;

    /**
     * Constructor instantiates a new <code>KeyRotateLeftAction</code> object.
     * 
     * @param camera
     *            the camera to rotate.
     * @param speed
     *            the speed at which to rotate.
     */
    public KeySpinLeftAction(Camera camera, float speed) {
        this.camera = camera;
        this.speed = speed;
    }

    public void performAction(InputActionEvent evt) {
        
        float x_l,y_l,z_l;
        DisplaySystem display = DisplaySystem.getDisplaySystem();
        // Detecta centro deslocado do foco de atenção
        Vector2f mouse_xy = new Vector2f(512,384);
        Vector3f worldCoords = display.getWorldCoordinates(mouse_xy, 0);
        Vector3f worldCoords2 = display.getWorldCoordinates(mouse_xy, 1);
        Vector3f direction = worldCoords2.subtractLocal(worldCoords).normalizeLocal();
        Ray mouseRay = new Ray(worldCoords, direction);
        float planeY = 0;
        float startY = mouseRay.origin.y;
        float endY = mouseRay.direction.y;
        float coef = (planeY - startY) / endY;
        float xo = mouseRay.origin.x + (coef * mouseRay.direction.x);
        float zo = mouseRay.origin.z + (coef * mouseRay.direction.z); 
        // Detecta circunferencia sobre o centro deslocado
        x_l = camera.getLocation().x-xo;
        y_l = camera.getLocation().y;
        z_l = camera.getLocation().z-zo;
        float L = (float) Math.sqrt( x_l * x_l + z_l * z_l);
        float ang = (float)Math.atan2(z_l, x_l);
        ang += 1f/180f * Math.PI;
        //System.out.println("y:"+y_l+" L:"+L);
        x_l = (float)(L*Math.cos(ang))+xo;
        z_l = (float)(L*Math.sin(ang))+zo;
        //System.out.println("xo:"+xo+" zo:"+zo+" x:"+x_l+" z:"+z_l);
        Vector3f newlocation = new Vector3f(x_l,y_l,z_l);
        camera.setLocation(newlocation);
        //System.out.println("newlocation:"+newlocation.toString());
        //camera.lookAt(new Vector3f(planeX,0,planeZ), new Vector3f(0,1f,0));
        Vector3f focusofattention = new Vector3f(xo,0,zo);
        //System.out.println("focusofattention:"+focusofattention.toString());
        Vector3f newdirection = focusofattention.subtract(newlocation);
        //System.out.println("newdirection(antes de normalizar):"+newdirection);
        newdirection = newdirection.normalize();
        //System.out.println("newdirection:"+newdirection);
        camera.setDirection(newdirection);
        Vector3f tangent = new Vector3f((float)(L*Math.cos(ang+Math.PI/2)+xo),y_l,(float)(L*Math.sin(ang+Math.PI/2)+zo));
        //System.out.println("tangent:"+tangent);
        Vector3f centerhigh = new Vector3f(xo,y_l,zo);
        Vector3f newleft = tangent.subtract(centerhigh);
        //System.out.println("newleft(antes de normalizar:"+newleft);
        newleft = newleft.normalize();
        //System.out.println("newleft:"+newleft);
        camera.setLeft(newleft);
        Vector3f newup = newdirection.cross(newleft);
        newup = newup.normalize();
        //System.out.println("newup:"+newup);
        camera.setUp(newup);
        //System.out.println("xd:"+camera.getLocation().x+" yd:"+camera.getLocation().y+" zd:"+camera.getLocation().z);
        
        camera.normalize();
        camera.update();
    }
}