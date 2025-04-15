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
 *    Klaus Raizer, Andre Paraense, Ricardo Ribeiro Gudwin
 *****************************************************************************/

package codelets.perception;



import br.unicamp.cst.core.entities.Codelet;
import br.unicamp.cst.core.entities.Memory;
import br.unicamp.cst.core.entities.MemoryObject;
import br.unicamp.cst.representation.idea.Idea;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;
import ws3dproxy.model.Thing;

/**
 * @author klaus
 *
 */
public class ClosestAppleDetector extends Codelet {

	private Memory knownMO;
	private Memory closestAppleMO;
	private Memory innerSenseMO;
	
        private List<Thing> known;

	public ClosestAppleDetector() {
            this.name = "ClosestAppleDetector";
	}


	@Override
	public void accessMemoryObjects() {
		this.knownMO=(MemoryObject)this.getInput("KNOWN_APPLES");
		this.innerSenseMO=(MemoryObject)this.getInput("INNER");
		this.closestAppleMO=(MemoryObject)this.getOutput("CLOSEST_APPLE");	
	}
	@Override
	public void proc() {
                Thing closest_apple=null;
                known = Collections.synchronizedList((List<Thing>) knownMO.getI());
                Idea cis = (Idea) innerSenseMO.getI();
                synchronized(known) {
		   if(known.size() != 0){
			//Iterate over objects in vision, looking for the closest apple
                        CopyOnWriteArrayList<Thing> myknown = new CopyOnWriteArrayList<>(known);
                        for (Thing t : myknown) {
				String objectName=t.getName();
				if(objectName.contains("PFood") && !objectName.contains("NPFood")){ //Then, it is an apple
                                        if(closest_apple == null){    
                                                closest_apple = t;
					}
                                        else {
						double Dnew = calculateDistance(t.getX1(), t.getY1(), (double)cis.get("position.x").getValue(), (double)cis.get("position.y").getValue());
                                                double Dclosest= calculateDistance(closest_apple.getX1(), closest_apple.getY1(), (double)cis.get("position.x").getValue(), (double)cis.get("position.y").getValue());
						if(Dnew<Dclosest){
                                                        closest_apple = t;
						}
					}
				}
			}
		   }
                }
//                if (closest_apple != null)
//                   System.out.println("Closest apple: "+closest_apple.getName()+" known: "+known.size());
//                else
//                   System.out.println("Closest apple: null"+" known: "+known.size()); 
                closestAppleMO.setI(closest_apple);
	}//end proc

@Override
        public void calculateActivation() {
        
        }
        
        private double calculateDistance(double x1, double y1, double x2, double y2) {
            return(Math.sqrt(Math.pow(x1-x2, 2)+Math.pow(y1-y2, 2)));
        }

}
