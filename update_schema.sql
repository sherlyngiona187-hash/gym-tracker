USE gym_management;

-- Disable foreign key checks temporarily
SET FOREIGN_KEY_CHECKS=0;

-- Drop foreign keys that reference member.Member_ID
ALTER TABLE attendance DROP FOREIGN KEY attendance_ibfk_1;
ALTER TABLE BODY_MEASUREMENT DROP FOREIGN KEY body_measurement_ibfk_1;
ALTER TABLE diet_plan DROP FOREIGN KEY fk_diet_member;
ALTER TABLE payment DROP FOREIGN KEY payment_ibfk_1;
ALTER TABLE workout_plan DROP FOREIGN KEY fk_workout_member;

-- Modify Member_ID to be AUTO_INCREMENT
ALTER TABLE member MODIFY Member_ID INT AUTO_INCREMENT;

-- Re-add foreign keys
ALTER TABLE attendance ADD CONSTRAINT attendance_ibfk_1 FOREIGN KEY (Member_ID) REFERENCES member (Member_ID);
ALTER TABLE BODY_MEASUREMENT ADD CONSTRAINT body_measurement_ibfk_1 FOREIGN KEY (Member_ID) REFERENCES member (Member_ID) ON UPDATE CASCADE;
ALTER TABLE diet_plan ADD CONSTRAINT fk_diet_member FOREIGN KEY (Member_ID) REFERENCES member (Member_ID) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE payment ADD CONSTRAINT payment_ibfk_1 FOREIGN KEY (Member_ID) REFERENCES member (Member_ID);
ALTER TABLE workout_plan ADD CONSTRAINT fk_workout_member FOREIGN KEY (Member_ID) REFERENCES member (Member_ID) ON DELETE CASCADE ON UPDATE CASCADE;

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS=1;
